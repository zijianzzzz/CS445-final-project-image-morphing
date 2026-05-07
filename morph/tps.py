import os

import cv2
import numpy as np

from morph.blend import laplacian_pyramid_blending


def _as_float_points(points):
    pts = np.asarray(points, dtype=np.float64)
    if pts.ndim != 2 or pts.shape[1] != 2:
        raise ValueError("Control points must have shape (N, 2).")
    return pts


def _kernel(r2):
    safe_r2 = np.maximum(r2, 1e-12)
    values = safe_r2 * np.log(safe_r2)
    values[r2 <= 1e-12] = 0.0
    return values


def solve_tps_parameters(source_points, target_points, regularization=1e-3):
    src = _as_float_points(source_points)
    dst = _as_float_points(target_points)

    if src.shape != dst.shape:
        raise ValueError("Source and target control points must have the same shape.")
    if src.shape[0] < 3:
        raise ValueError("Thin Plate Spline requires at least 3 control points.")

    n_points = src.shape[0]
    diff = src[:, None, :] - src[None, :, :]
    r2 = np.sum(diff * diff, axis=2)
    k_matrix = _kernel(r2)
    k_matrix += np.eye(n_points) * regularization

    p_matrix = np.concatenate((np.ones((n_points, 1)), src), axis=1)
    upper = np.concatenate((k_matrix, p_matrix), axis=1)
    lower = np.concatenate((p_matrix.T, np.zeros((3, 3))), axis=1)
    system = np.concatenate((upper, lower), axis=0)

    rhs_x = np.concatenate((dst[:, 0], np.zeros(3)))
    rhs_y = np.concatenate((dst[:, 1], np.zeros(3)))

    params_x = np.linalg.solve(system, rhs_x)
    params_y = np.linalg.solve(system, rhs_y)

    return {
        "control_points": src,
        "weights_x": params_x[:n_points],
        "affine_x": params_x[n_points:],
        "weights_y": params_y[:n_points],
        "affine_y": params_y[n_points:],
    }


def evaluate_tps_map(parameters, query_points):
    ctrl = parameters["control_points"]
    query = _as_float_points(query_points)

    diff = query[:, None, :] - ctrl[None, :, :]
    r2 = np.sum(diff * diff, axis=2)
    basis = _kernel(r2)
    affine = np.concatenate((np.ones((query.shape[0], 1)), query), axis=1)

    mapped_x = basis @ parameters["weights_x"] + affine @ parameters["affine_x"]
    mapped_y = basis @ parameters["weights_y"] + affine @ parameters["affine_y"]

    return np.stack((mapped_x, mapped_y), axis=1)


def get_intermediate_points(source_points, target_points, k, n):
    src = _as_float_points(source_points)
    dst = _as_float_points(target_points)
    alpha = k / n
    return (1.0 - alpha) * src + alpha * dst


def _build_rect_border(
    top,
    bottom,
    left,
    right,
    points_per_edge=12,
):
    if points_per_edge < 2:
        raise ValueError("Face rectangle border needs at least 2 points per edge.")

    rows = np.linspace(top, bottom, points_per_edge)
    cols = np.linspace(left, right, points_per_edge)

    border = []
    for col in cols:
        border.append((top, col))
    for row in rows[1:]:
        border.append((row, right))
    for col in cols[-2::-1]:
        border.append((bottom, col))
    for row in rows[-2:0:-1]:
        border.append((row, left))

    return np.asarray(border, dtype=np.float64)


def _clip_rect(top, bottom, left, right, image_shape):
    height, width = image_shape[:2]
    return (
        max(0.0, top),
        min(float(height - 1), bottom),
        max(0.0, left),
        min(float(width - 1), right),
    )


def _build_rect_border_rings(
    top,
    bottom,
    left,
    right,
    image_shape,
    points_per_edge=12,
    ring_count=4,
    ring_step_ratio=0.08,
):
    if ring_count < 1:
        raise ValueError("Face rectangle border needs at least one ring.")

    rect_height = bottom - top
    rect_width = right - left
    ring_step = max(rect_height, rect_width) * ring_step_ratio
    ring_step = max(ring_step, 6.0)

    borders = []
    for ring_idx in range(ring_count):
        pad = ring_idx * ring_step
        ring_top, ring_bottom, ring_left, ring_right = _clip_rect(
            top - pad,
            bottom + pad,
            left - pad,
            right + pad,
            image_shape,
        )
        if ring_top < ring_bottom and ring_left < ring_right:
            borders.append(
                _build_rect_border(
                    ring_top,
                    ring_bottom,
                    ring_left,
                    ring_right,
                    points_per_edge=points_per_edge,
                )
            )

    return np.concatenate(borders, axis=0)


def select_face_rect_border(image, window_name, points_per_edge=12):
    clicks = []

    def draw_preview():
        shown = image.copy()
        cv2.putText(
            shown,
            "Click upper-left and lower-right corners",
            (10, 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            shown,
            "R: reset   Esc/Enter: finish",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )
        for row, col in clicks:
            cv2.circle(shown, (int(col), int(row)), 3, (0, 255, 255), -1)
        if len(clicks) == 2:
            row1, col1 = clicks[0]
            row2, col2 = clicks[1]
            top = int(min(row1, row2))
            bottom = int(max(row1, row2))
            left = int(min(col1, col2))
            right = int(max(col1, col2))
            cv2.rectangle(shown, (left, top), (right, bottom), (0, 255, 255), 2)
            rect_height = bottom - top
            rect_width = right - left
            ring_step = max(max(rect_height, rect_width) * 0.08, 6.0)
            for ring_idx in range(1, 4):
                pad = int(round(ring_idx * ring_step))
                ring_top = max(0, top - pad)
                ring_bottom = min(image.shape[0] - 1, bottom + pad)
                ring_left = max(0, left - pad)
                ring_right = min(image.shape[1] - 1, right + pad)
                cv2.rectangle(shown, (ring_left, ring_top), (ring_right, ring_bottom), (0, 180, 255), 1)
        return shown

    def on_click(event, x, y, flags, param):
        if event != cv2.EVENT_LBUTTONDOWN:
            return
        if len(clicks) == 2:
            clicks.clear()
        clicks.append((y, x))

    print(
        f"Select rectangular face border for {window_name}. "
        "Click the upper-left and lower-right rectangle corners, then press Enter or Esc. Press R to reset."
    )
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, on_click)

    while True:
        cv2.imshow(window_name, draw_preview())
        key = cv2.waitKey(20) & 0xFF
        if key in (ord("r"), ord("R")):
            clicks.clear()
        elif key in (13, 27):
            break

    cv2.destroyWindow(window_name)
    if len(clicks) != 2:
        raise ValueError("TPS face border selection requires two rectangle corner clicks.")

    row1, col1 = clicks[0]
    row2, col2 = clicks[1]
    top = float(min(row1, row2))
    bottom = float(max(row1, row2))
    left = float(min(col1, col2))
    right = float(max(col1, col2))

    if top == bottom or left == right:
        raise ValueError("TPS face border rectangle must have non-zero width and height.")

    return _build_rect_border_rings(
        top,
        bottom,
        left,
        right,
        image.shape,
        points_per_edge=points_per_edge,
    )


def _append_points(points, extra_points):
    pts = _as_float_points(points)
    extra = _as_float_points(extra_points)
    if extra.shape[0] == 0:
        return pts
    return np.concatenate((pts, extra), axis=0)


def add_face_border_correspondences(img1, img2, points1, points2):
    border1 = select_face_rect_border(img1, "source TPS face border")
    border2 = select_face_rect_border(img2, "destination TPS face border")
    print(f"Added {border1.shape[0]} manually selected rectangular face border points to TPS.")
    return _append_points(points1, border1), _append_points(points2, border2)


def add_multi_face_border_correspondences(imgs, point_sets):
    border_sets = [
        select_face_rect_border(img, f"image {idx} TPS face border")
        for idx, img in enumerate(imgs)
    ]

    border_count = border_sets[0].shape[0]
    print(f"Added {border_count} manually selected rectangular face border points to every TPS image.")
    return [
        _append_points(points, border)
        for points, border in zip(point_sets, border_sets)
    ]


def _build_query_grid(height, width):
    rows, cols = np.indices((height, width), dtype=np.float64)
    return np.stack((rows.ravel(), cols.ravel()), axis=1)


def _sample_image_bilinear(image, sample_points):
    height, width = image.shape[:2]

    rows = np.clip(sample_points[:, 0], 0, height - 1)
    cols = np.clip(sample_points[:, 1], 0, width - 1)

    row0 = np.floor(rows).astype(np.int32)
    col0 = np.floor(cols).astype(np.int32)
    row1 = np.clip(row0 + 1, 0, height - 1)
    col1 = np.clip(col0 + 1, 0, width - 1)

    dr = rows - row0
    dc = cols - col0

    top_left = image[row0, col0].astype(np.float64)
    top_right = image[row0, col1].astype(np.float64)
    bottom_left = image[row1, col0].astype(np.float64)
    bottom_right = image[row1, col1].astype(np.float64)

    top = (1.0 - dc)[:, None] * top_left + dc[:, None] * top_right
    bottom = (1.0 - dc)[:, None] * bottom_left + dc[:, None] * bottom_right
    return (1.0 - dr)[:, None] * top + dr[:, None] * bottom


def warp_image_with_tps(image, source_points, target_points, regularization=1e-3):
    height, width = image.shape[:2]
    params = solve_tps_parameters(target_points, source_points, regularization=regularization)
    query = _build_query_grid(height, width)
    sample_points = evaluate_tps_map(params, query)
    warped = _sample_image_bilinear(image, sample_points)
    return warped.reshape(height, width, image.shape[2])


def warp_image_tps_with_linear_dissolve(
    no_of_intermed,
    img1,
    img2,
    points1,
    points2,
    output_dir="generated-images/tps-linear-dissolve",
):
    n = no_of_intermed + 2
    os.makedirs(output_dir, exist_ok=True)
    frame_paths = []
    points1, points2 = add_face_border_correspondences(img1, img2, points1, points2)

    for k in range(1, no_of_intermed + 1):
        print(str(k) + " TPS intermediate is generating. Please wait...")
        intermediate_points = get_intermediate_points(points1, points2, k, n)
        img1_warp = warp_image_with_tps(img1, points1, intermediate_points)
        img2_warp = warp_image_with_tps(img2, points2, intermediate_points)
        alpha = k / n
        inter = (1.0 - alpha) * img1_warp + alpha * img2_warp
        inter = np.clip(inter, 0, 255).astype(np.uint8)

        name = os.path.join(output_dir, "inter_" + str(k) + ".jpg")
        cv2.imwrite(name, inter)
        frame_paths.append(name)

    return frame_paths


def warp_image_tps_with_laplacian_pyramid_blending(
    no_of_intermed,
    img1,
    img2,
    points1,
    points2,
    output_dir="generated-images/tps-laplacian-pyramid-blending",
):
    n = no_of_intermed + 2
    os.makedirs(output_dir, exist_ok=True)
    frame_paths = []
    points1, points2 = add_face_border_correspondences(img1, img2, points1, points2)

    for k in range(1, no_of_intermed + 1):
        print(str(k) + " TPS intermediate is generating. Please wait...")
        intermediate_points = get_intermediate_points(points1, points2, k, n)
        img1_warp = warp_image_with_tps(img1, points1, intermediate_points)
        img2_warp = warp_image_with_tps(img2, points2, intermediate_points)
        alpha = k / n
        inter = laplacian_pyramid_blending(img1_warp, img2_warp, alpha)
        inter = np.clip(inter, 0, 255).astype(np.uint8)

        name = os.path.join(output_dir, "inter_" + str(k) + ".jpg")
        cv2.imwrite(name, inter)
        frame_paths.append(name)

    return frame_paths


def warp_image_tps_transform_multiple_imgs(
    no_of_intermed,
    imgs,
    point_sets,
    output_dir="generated-images/multi-input-tps-linear-dissolve",
    blend="linear",
):
    if len(imgs) != len(point_sets):
        raise ValueError("Multi-image TPS requires one control-point set per image.")
    if len(imgs) < 2:
        raise ValueError("Multi-image TPS requires at least two images.")

    point_count = len(point_sets[0])
    if point_count < 3:
        raise ValueError("Thin Plate Spline requires at least 3 control points.")
    if any(len(points) != point_count for points in point_sets):
        raise ValueError("Every multi-image TPS control-point set must have the same number of points.")

    point_sets = add_multi_face_border_correspondences(imgs, point_sets)

    os.makedirs(output_dir, exist_ok=True)
    frame_paths = []
    frame_count = 0
    n = no_of_intermed + 2

    for image_idx in range(len(imgs) - 1):
        img1 = imgs[image_idx]
        img2 = imgs[image_idx + 1]
        points1 = point_sets[image_idx]
        points2 = point_sets[image_idx + 1]

        for k in range(1, no_of_intermed + 1):
            print(
                str(k)
                + f" TPS intermediate of image{image_idx} and image{image_idx + 1} is generating. Please wait..."
            )
            intermediate_points = get_intermediate_points(points1, points2, k, n)
            img1_warp = warp_image_with_tps(img1, points1, intermediate_points)
            img2_warp = warp_image_with_tps(img2, points2, intermediate_points)
            alpha = k / n
            if blend == "laplacian":
                inter = laplacian_pyramid_blending(img1_warp, img2_warp, alpha)
            else:
                inter = (1.0 - alpha) * img1_warp + alpha * img2_warp
            inter = np.clip(inter, 0, 255).astype(np.uint8)

            name = os.path.join(output_dir, "inter_" + str(frame_count) + ".jpg")
            cv2.imwrite(name, inter)
            frame_paths.append(name)
            frame_count += 1

    return frame_paths
