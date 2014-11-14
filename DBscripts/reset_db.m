%reset db tables below recordings
dbname='vp_sldata';
CCNdb = connect2DB(dbname);
            
exec(CCNdb, 'ALTER TABLE stats DROP FOREIGN KEY stats_ibfk_1');
exec(CCNdb, 'ALTER TABLE stats DROP FOREIGN KEY stats_ibfk_2');
exec(CCNdb, 'ALTER TABLE psth DROP FOREIGN KEY psth_ibfk_1');
exec(CCNdb, 'ALTER TABLE clusters DROP FOREIGN KEY clusters_ibfk_1');
exec(CCNdb, 'ALTER TABLE sorts DROP FOREIGN KEY sorts_ibfk_1');

exec(CCNdb, 'TRUNCATE TABLE stats');
exec(CCNdb, 'TRUNCATE TABLE psth');
exec(CCNdb, 'TRUNCATE TABLE clusters');
exec(CCNdb, 'TRUNCATE TABLE sorts');

exec(CCNdb, 'ALTER TABLE stats AUTO_INCREMENT=1');
exec(CCNdb, 'ALTER TABLE psth AUTO_INCREMENT=1');
exec(CCNdb, 'ALTER TABLE clusters AUTO_INCREMENT=1');
exec(CCNdb, 'ALTER TABLE sorts AUTO_INCREMENT=1');

exec(CCNdb, 'ALTER TABLE stats ADD CONSTRAINT `stats_ibfk_1` FOREIGN KEY (`psth_id_fk`) REFERENCES `psth` (`psth_id`) ON UPDATE CASCADE');
exec(CCNdb, 'ALTER TABLE stats ADD CONSTRAINT `stats_ibfk_2` FOREIGN KEY (`cluster_id_fk`) REFERENCES `clusters` (`cluster_id`) ON DELETE CASCADE ON UPDATE CASCADE');
exec(CCNdb, 'ALTER TABLE psth ADD CONSTRAINT `psth_ibfk_1` FOREIGN KEY (cluster_id_fk) REFERENCES clusters (cluster_id) ON DELETE CASCADE ON UPDATE CASCADE');
exec(CCNdb, 'ALTER TABLE clusters ADD CONSTRAINT `clusters_ibfk_1` FOREIGN KEY (`sort_id_fk`) REFERENCES `sorts` (`sort_id`) ON DELETE CASCADE ON UPDATE CASCADE');
exec(CCNdb, 'ALTER TABLE sorts ADD CONSTRAINT `sorts_ibfk_1` FOREIGN KEY (`recording_id_fk`) REFERENCES `recordings` (`recording_id`) ON DELETE CASCADE ON UPDATE CASCADE');

