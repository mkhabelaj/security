DROP TABLE IF EXISTS config;
DROP TABLE IF EXISTS port_map;

CREATE TABLE IF NOT EXISTS port_map(
  stream_secret VARCHAR(255) NOT NULL PRIMARY KEY,
  camera_number INTEGER NOT NULL,
  socket_server_port INTEGER NOT NULL ,
  websocket_server_port INTEGER NOT NULL ,
  ip_address VARCHAR(255) NOT NULL DEFAULT 'localhost'
);

CREATE TABLE IF NOT EXISTS config(
    camera_name VARCHAR(255) DEFAULT 'default cam name',
    show_video BOOLEAN NOT NULL DEFAULT FALSE,
    record_motion BOOLEAN NOT NULL DEFAULT FALSE,
    capture_image BOOLEAN NOT NULL DEFAULT FALSE,
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
    display_text_if_unoccupied VARCHAR(255) NOT NULL DEFAULT 'Unoccupied',
    stream_key VARCHAR(255) REFERENCES port_map (stream_secret)
);


