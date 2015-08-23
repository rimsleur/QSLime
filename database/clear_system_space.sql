DELETE FROM qsl_error;
DELETE FROM qsl_language;
DELETE FROM qsl_concept WHERE id < 100;
ALTER TABLE qsl_concept AUTO_INCREMENT=1;
DELETE FROM qsl_linkage WHERE id < 100;
ALTER TABLE qsl_linkage AUTO_INCREMENT=1;