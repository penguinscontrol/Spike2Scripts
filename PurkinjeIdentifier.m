clear;clc;
cd('E:\\Spike_Sorting\\spike2temp\\');

load('postss.mat'); % post simple spike data

tn1 = whos; % temporary name holder
tn2 = tn1.name;

eval(['datastr = ', tn2,';']); % get data as a struct
data = datastr.values;
data = data';


data_fft = fft(data);
[rws,cls] = size(data_fft);
data_fft_amp = abs(data_fft(2:(floor(rws/2)+1),:)); %get fft amplitudes, minus DC offset

data_fft_amp_maxes = max(data_fft_amp);