function [ success, sort_id ] = addSort( newsort, conn )
%addSort appends a new sort to the DB
try
    [col_names, this_data] = dataFromSort(newsort);
    datainsert(conn,'sorts',col_names, this_data);
    commit(conn);
    query = 'SELECT LAST_INSERT_ID()';           
    results = fetch(conn, query);
    sort_id = results{1};
    success = 1;
catch
        success = 0;
        sort_id = nan;
end

end

