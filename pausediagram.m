function  pausediagram( times, labels )
times = times.*1000; % seconds to miliseconds conversion
clus_names = unique(labels); % Names of clusters

if length(clus_names) ~= 2
    error('Incompatible cluster labels, aborting...');
end

ss_label = clus_names(1); % Simple spike labels
cs_label = clus_names(2); % Complex spike labels
no_cs = sum(labels == cs_label); % number of CS

cs_times = times(labels == cs_label);
post_cs = cell(1,no_cs);

for a = 1:no_cs
    if a < no_cs
        temp_times = times(times > cs_times(a) & times<cs_times(a+1));
        post_cs{a} = temp_times-cs_times(a);
    else
        temp_times = times(times > cs_times(a));
        post_cs{a} = temp_times-cs_times(a);
    end
end

maxtimes = cellfun(@max,post_cs,'UniformOutput', false);
maxtimes = maxtimes(~cellfun(@isempty,maxtimes));
bins = 0:max(cell2mat(maxtimes))+1;

raster_lines = zeros(no_cs, length(bins));
for a = 1:no_cs
    raster_lines(a,:) = hist(post_cs{a},bins);
end

raster_lines = raster_lines(:,1:100);

[indy, indx] = ind2sub(size(raster_lines),find(raster_lines)); %find row and column coordinates of spikes
        %indy = -indy+size(cut_rasters,1); % flip so that the top raster plots on the top
        
            if(size(raster_lines,1) == 1)
                plot([indx;indx],[indy;indy+1],'k.','MarkerSize',10); % plot rasters
            else
                plot([indx';indx'],[indy';indy'+1],'k.','MarkerSize',10); % plot rasters
            end
            
hold on;
sdf = sum(raster_lines); sdf = size(raster_lines,1).*0.5.*sdf./(max(sdf));
plot(1:100,sdf,'LineWidth',5);
end