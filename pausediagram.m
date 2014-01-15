function  pausediagram( times, labels )

clus_names = unique(labels); % Names of clusters

if length(clus_names) ~= 2
    error('Incompatible cluster labels, aborting...');
end

ss_label = clus_names(1); % Simple spike labels
cs_label = clus_names(2); % Complex spike labels
no_cs = sum(labels == cs_label); % number of CS

cs_times = times(labels == cs_label);
post_cs = cell(1,no_cs);
raster_lines = cell(1,no_cs);

for a = 1:no_cs
    if a < no_cs
        post_cs{a} = (times(times > cs_times(a) & times<cs_times(a+1))-cs_times(a)).*1000;
    else
        post_cs{a} = (times(times > cs_times(a))-cs_times(a)).*1000;
    end
end

maxtimes = cellfun(@max,post_cs,'UniformOutput', false);
maxtime = max(cell2mat(maxtimes(~isempty(maxtimes))));
bins = 0:maxtime+1;

for a = 1:no_cs
    raster_lines{a} = hist(post_cs{a},bins);
end

end