create table config(
    show_video INTEGER DEFAULT 1 NOT NULL,
    record_motion INTEGER DEFAULT 0 NOT NULL,
    min_upload_seconds INTEGER,
    min_motion_frames INTEGER,
    delta_thresh INTEGER,
    motion_detection INTEGER  DEFAULT 0 NOT NULL,
    min_email_seconds INTEGER,
    email_images INTEGER  DEFAULT 0 NOT NULL,
    min_area INTEGER NOT NULL,
    display_text_if_occupied VARCHAR(255) NOT NULL DEFAULT 'Occupied',
    display_text_if_unoccupied VARCHAR(255) NOT NULL DEFAULT 'Unoccupied'
);

INSERT INTO config (
  min_upload_seconds,
  min_motion_frames,
  delta_thresh,
  min_email_seconds,
  min_area)
VALUES (1,1,5,3,5000);
