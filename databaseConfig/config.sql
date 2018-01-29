DROP TABLE IF EXISTS config;

CREATE TABLE IF NOT EXISTS config(
    show_video BOOLEAN NOT NULL DEFAULT FALSE,
    record_motion BOOLEAN NOT NULL DEFAULT FALSE,
    min_upload_seconds INTEGER,
    min_motion_frames INTEGER,
    delta_thresh INTEGER,
    motion_detection BOOLEAN NOT NULL DEFAULT TRUE,
    min_email_seconds INTEGER,
    email_images BOOLEAN NOT NULL DEFAULT FALSE,
    min_area INTEGER NOT NULL,
    resolution_width INTEGER NOT NULL,
    resolution_height INTEGER NOT NULL,
    display_text_if_occupied VARCHAR(255) NOT NULL DEFAULT 'Occupied',
    display_text_if_unoccupied VARCHAR(255) NOT NULL DEFAULT 'Unoccupied'
);

INSERT INTO config (
  min_upload_seconds,
  min_motion_frames,
  delta_thresh,
  min_email_seconds,
  min_area,
  resolution_width,
  resolution_height)
VALUES (1 ,1, 5, 3, 5000, 640, 480);

DROP TABLE IF EXISTS port_map;

CREATE TABLE IF NOT EXISTS port_map(
  camera_number INTEGER NOT NULL,
  socket_server_port INTEGER NOT NULL ,
  websocket_server_port INTEGER NOT NULL ,
  stream_secret VARCHAR(255) NOT NULL,
  ip_address VARCHAR(255) NOT NULL DEFAULT 'localhost'
);
