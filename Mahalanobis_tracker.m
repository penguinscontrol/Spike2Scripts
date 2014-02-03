

% Variables from Spike2, uncomment for debugging
%  clear;clc;close all;
%  pulse_clus = 1;
%  timelength = 1238.54678;
%  tsamp = 2e-5;
%  temp_size = 35;
%  start_offset = 10;
 comps = [1 2 3];

if strcmp(getenv('username'),'DangerZone')
        directory = 'E:\data\Recordings\';
    elseif strcmp(getenv('username'),'Radu')
        directory = 'E:\Spike_Sorting\';
    elseif strcmp(getenv('username'),'The Doctor')
        directory = 'C:\Users\The Doctor\Data\';
    elseif strcmp(getenv('username'),'JuanandKimi') || ...
            strcmp(getenv('username'),'Purkinje')
        directory = 'C:\Data\Recordings\';
    else
        directory = 'B:\data\Recordings\';
end

cd([directory, 'spike2temp\']);

plot_mahalanobis('mahala.mat',temp_size, start_offset,pulse_clus,comps);