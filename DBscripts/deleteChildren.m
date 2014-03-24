function success = deleteChildren( sort_id, conn, ftp_conn )
%deleteChildren of a sort when it's updated, clusters and psth's

results = fetch(conn, ['SELECT cluster_id, average_wvfrm, isi FROM clusters c WHERE c.sort_fid =' num2str(sort_id)]);
psths = {};

for a = 1:size(results,1)
    end

cd(ftp_conn,'/myapp/figures/');
for a = 1:size(results,1)
    psths =  [psths fetch(conn, ['SELECT psth_id, image_url FROM psth p WHERE p.cluster_fid =' num2str(results{a})])];
    sqlquery = ['DELETE FROM psth WHERE psth.cluster_fid = ' num2str(results{a})];
    curs = exec(conn, sqlquery);
    
    try
        delete(ftp_conn,results{a,2});
        delete(ftp_conn,results{a,3});
    catch
        disp('Nothing to delete!');
    end
end

for a = 1:size(psths,1)
    try
        delete(ftp_conn,psths{a,2});
    catch
        disp('Nothing to delete!');
    end
end

sqlquery = ['DELETE FROM clusters WHERE sort_fid = ' num2str(sort_id)];
curs = exec(conn, sqlquery);

end