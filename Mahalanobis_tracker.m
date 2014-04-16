% Variables from Spike2, uncomment for debugging
%  clear;clc;close all;
%  pulse_clus = 0;
%  timelength = 89.9119;
%  tsamp = 2e-5;
%  temp_size = 32;
%  sigma = 1;
%  start_offset = 12;
%  fname = 'testing_mahala';

% if strcmp(getenv('username'),'DangerZone')
%         directory = 'E:\data\Recordings\';
%     elseif strcmp(getenv('username'),'Radu')
%         directory = 'E:\Spike_Sorting\';
%     elseif strcmp(getenv('username'),'The Doctor')
%         directory = 'C:\Users\The Doctor\Data\';
%     elseif strcmp(getenv('username'),'JuanandKimi') || ...
%             strcmp(getenv('username'),'Purkinje')
%         directory = 'C:\Data\Recordings\';
%     else
%         directory = 'B:\data\Recordings\';
% end

cd([directory, 'spike2temp\']);
sigma = 1000.*sigma; % Convert sigma from seconds to milliseconds
comps = [1 2 3]; % Which components to look at?
clusternames = plot_mahalanobis('mahala.mat',double(temp_size),double(start_offset),double(pulse_clus),comps,sigma,1);

cd([directory, 'figures\']);
figs = get(0, 'Children'); % Get all figures
figs = figs(length(figs):-1:1);
for a = 1:length(figs)
    figure(figs(a));
    set(gcf, 'Color', 'none',...
    'PaperUnits','inches',...
    'PaperPosition', [0.1 0.1 2.9 4.9],...
    'PaperSize', [3 5]);
    print('-dpng',[fname '_Mahtrack_cl_' num2str(clusternames(a))]);
end