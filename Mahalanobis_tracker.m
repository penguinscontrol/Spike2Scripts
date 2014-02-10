
<<<<<<< HEAD
% 
% % Variables from Spike2, uncomment for debugging
%  clear;clc;close all;
%  pulse_clus = 0;
%  timelength = 89.9119;
%  tsamp = 2e-5;
%  temp_size = 32;
%  sigma = 1;
%  start_offset = 12;
=======

%  % Variables from Spike2, uncomment for debugging
%   clear;clc;close all;
%   pulse_clus = 0;
%   timelength = 89.9119;
%   tsamp = 2e-5;
%   temp_size = 32;
%   start_offset = 12;
>>>>>>> dff5ef96fb8aab8ef586696694ebd9029b303b2c

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
<<<<<<< HEAD
sigma = 1000.*sigma; % Convert sigma from seconds to milliseconds
comps = [1 2 3]; % Which components to look at?
plot_mahalanobis('mahala.mat',double(temp_size),double(start_offset),double(pulse_clus),comps,sigma,1);
=======

sigma = 5;
comps = [1 2 3]; % Which components to look at?
plot_mahalanobis('mahala.mat',double(temp_size),double(start_offset),double(pulse_clus),comps,sigma);
>>>>>>> dff5ef96fb8aab8ef586696694ebd9029b303b2c
