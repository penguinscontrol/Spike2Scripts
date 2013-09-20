function [ out ] = clus_mahalanobis(in,c1,c2,trigs,comps)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
load(in);
eval('dataname = who;');
eval(['data = ', dataname{1}]);

cluscodes = double(data.codes(:,1));
clusnames = unique(cluscodes);

clus = cell(length(clusnames),1);

pc_values = data.values(:,trigs(1):trigs(2));
[coeff, score] = princomp(pc_values);

a = 1;
for a = 1:length(clusnames)
    b = clusnames(a);
    clus{a} = struct('times',data.times(cluscodes == b),...
        'scores', score(cluscodes == b,:));
end

figure();
plot3(clus{clusnames == c1}.scores(:,comps(1)),clus{clusnames == c1}.scores(:,comps(2)),...
    clus{clusnames == c1}.scores(:,comps(3)),'bo');
hold on;
plot3(clus{clusnames == c2}.scores(:,comps(1)),clus{clusnames == c2}.scores(:,comps(2)),...
    clus{clusnames == c2}.scores(:,comps(3)),'r*');

pca_c1 = clus{clusnames == c1}.scores(:,comps);
pca_c2 = clus{clusnames == c2}.scores(:,comps);
d = mahal(pca_c2,pca_c1);
out = mean(d);

c1_box = MBoxtest(pca_c1)
end