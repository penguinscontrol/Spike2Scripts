function [ success ] = updateSort(s_id, newsort, conn)
%updateSort Summary of this function goes here
%   Detailed explanation goes here
success = 0;
try
    
    [col_names, this_data] = dataFromSort(newsort);
    this_data{1} = s_id;
    update(conn,'sorts',col_names,this_data,['WHERE sort_id = ' num2str(s_id) ';']);
    commit(conn);
    success = 1;
    sort_id = s_id;
catch
    
        success = 0;
        sort_id = nan;
end
end

