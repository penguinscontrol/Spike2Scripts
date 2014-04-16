function comps = plot_predictPCA(in, temp_size, start_offset, plotting_vis)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
load(in);
eval('dataname = who;');
eval(['data = ', dataname{1}]);

cluscodes = double(data.codes(:,1)); % vector listing codes for each waveform
clusnames = unique(cluscodes);  % list of all distinct names
clusnames(clusnames == 0) = []; % we need code 0 in here for PCA, but will not examine

trigs = [start_offset start_offset+temp_size]; % what part of the full waveform to do PCA on
pc_values = data.values(:,trigs(1):trigs(2)); % truncate the waveform for PCA
[coeff, score] = princomp(pc_values); % scores and components

h = zeros(size(score,2),1);
kstat = zeros(size(score,2),1);
rest_scores = cell(size(score,2),1);
for a = 1:size(score,2)
    thesescores = score(:,a);
    [muhat, sigmahat] = normfit(thesescores);
    thesescores = thesescores(thesescores > (muhat-3.*sigmahat) &... 
    thesescores < (muhat+3.*sigmahat));
    [thish, ~, thisk] = lillietest(thesescores);
    h(a) = thish;
    kstat(a) = thisk;
    rest_scores{a} = thesescores;
end

comps = find(h == 1);
kstat = kstat(comps);
[~,ind] = sort(kstat,'descend');

comps = comps(ind(1:3));
comps = sort(comps);
figure();

plocs = [1 3 5];
for a = 1:length(comps)
subplot(3,2,plocs(a));
hist(rest_scores{comps(a)},100);
title(sprintf('Score distribution for component %d',comps(a)));
end

subplot(1,2,2);
plot3(score(:,comps(1)),score(:,comps(2)),score(:,comps(3)),'k.');
xlabel(sprintf('Component %d score',comps(1)));

ylabel(sprintf('Component %d score',comps(2)));

zlabel(sprintf('Component %d score',comps(3)));
end