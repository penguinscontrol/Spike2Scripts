function clus = plot_mahalanobis(in, temp_size, start_offset, pulse_clus,comps, sigma,plotting_vis)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
load(in);
eval('dataname = who;');
eval(['data = ', dataname{1}]);

cluscodes = double(data.codes(:,1)); % vector listing codes for each waveform
clusnames = unique(cluscodes);  % list of all distinct names
clusnames(clusnames == 0) = []; % we need code 0 in here for PCA, but will not examine

if pulse_clus ~= 0
    clusnames(clusnames == pulse_clus) = []; % take out the tms artifact
end

trigs = [start_offset start_offset+temp_size]; % what part of the full waveform to do PCA on
pc_values = data.values(:,trigs(1):trigs(2)); % truncate the waveform for PCA
[coeff, score] = princomp(pc_values); % scores and components


clus = cell(length(clusnames),1); % will hold times and PCA scores for each cluster
gauss_fits = cell(length(clusnames),1); % will hold the parameters of
                                        % the multivariate gaussian
                                        % approximating the clusters
score_mask = ismember(1:size(score,2),comps); % which components are we using?
                                              % i.e., which component space
                                              % to calculate mahalanobis
                                              % distance in

for a = 1:length(clusnames) % populate clus with times and PCA scores for each cluster
    b = clusnames(a); % current cluster name
    clus{a} = struct('times',round(data.times(cluscodes == b).*1000),... % times of that clus in ms
        'scores', score(cluscodes == b,score_mask),'mahal_distance',[],'mean_wave',[]);
    gauss_fits{a} = gmdistribution.fit(clus{a}.scores,1); % multivariate fit to that cluster
    clus{a}.mahal_distance = mahal(gauss_fits{a},clus{a}.scores);    % calculate distances from data points to center of fit
    clus{a}.mean_wave = mean(pc_values(cluscodes == b,:));
end

for a = 1:length(clusnames) % for each cluster, plot distance from center and scores through time
    figure();
    count_plots = length(comps)+1; % one subplot for each component plus the mahal dist
    cur_plot = 1; % current subplot window
    if plotting_vis % plot the visual cluster, first two components specified in comps[]
        whichtoplot = randperm(size(clus{a}.scores,1)); % Choose at most 500 points in this view to speed it up
        whichtoplot = whichtoplot(1:min(5e2,size(clus{a}.scores,1)));
        count_plots = count_plots+1; % add a plot for the gaussian fit
        score_mask = ismember(1:size(score,2),comps(1:2)); %restrict to first two components only
        gauss_fits_4plot = cell(length(clusnames),1);
        for c = 1:length(clusnames) 
            b = clusnames(c); % current cluster name
            gauss_fits_4plot{c} = gmdistribution.fit(score(cluscodes == b,score_mask),1); % multivariate fit to that cluster
        end
        subplot(count_plots,1,cur_plot);
        h(cur_plot) = plot(clus{a}.scores(whichtoplot,1),clus{a}.scores(whichtoplot,2),'k.','MarkerSize',5); % scatter plot of cluster in first 2 components space
        hold on;
        x_limits = [gauss_fits_4plot{a}.mu(1)-4.*sqrt(gauss_fits_4plot{a}.Sigma(1,1))...
            gauss_fits_4plot{a}.mu(1)+4.*sqrt(gauss_fits_4plot{a}.Sigma(1,1))];
        % 4 standard deviations on either side of the mean
        y_limits = [gauss_fits_4plot{a}.mu(2)-4.*sqrt(gauss_fits_4plot{a}.Sigma(2,2))...
            gauss_fits_4plot{a}.mu(2)+4.*sqrt(gauss_fits_4plot{a}.Sigma(2,2))];
    
        ezcontour(@(x,y)pdf(gauss_fits_4plot{a},[x y]),x_limits,y_limits);
        title(sprintf('Cluster %d: X axis: Component %d score Y axis: Component %d score',clusnames(a),comps(1),comps(2)));
        cur_plot = cur_plot+1;
    end
    padded_time = clus{a}.times(1):clus{a}.times(end); % add entries for all intermediate times, for smoothing
    padded_mahal = zeros(length(padded_time),1); % add zeros for smoothing
    padded_mahal(ismember(padded_time,clus{a}.times))=clus{a}.mahal_distance;
    sdf=fullgauss_filtconv(padded_mahal, sigma, 0); % smoothed
    sdf=sdf./max(sdf).*(max(clus{a}.mahal_distance).*0.4);
    subplot(count_plots,1,cur_plot);
    h(cur_plot) = plot(clus{a}.times, clus{a}.mahal_distance, 'k.','MarkerSize',5);
        title(['X axis: Time (ms) Y axis: Mahalanobis Distance using Components ' sprintf('%d ',comps')]);
    hold on;
    plot(padded_time, sdf, 'r-','LineWidth',5);
    cur_plot = cur_plot+1;
    
    for c = 1:length(comps) % plot all scores through time as well
        subplot(count_plots,1,cur_plot);
        these_scores = clus{a}.scores(:,c)-mean(clus{a}.scores(:,c)); % normalize scores to 0 mean for aesthetics
        h(cur_plot) = plot(clus{a}.times, these_scores, 'k.','MarkerSize',5);
        hold on;
        padded_score = zeros(length(padded_time),1);
        padded_score(ismember(padded_time,clus{a}.times))=these_scores;
        sdf=fullgauss_filtconv(padded_score, sigma, 0);
        sdf=sdf./max(sdf).*(max([these_scores;abs(these_scores)]).*0.4);
        plot(padded_time, sdf, 'r-','LineWidth',3);
        title(sprintf('X axis: Time (ms) Y axis: Component %d score',comps(c)));
        cur_plot = cur_plot+1;
    end
    figure();
    plot(clus{a}.mean_wave);
end

end