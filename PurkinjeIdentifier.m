
if strcmp(getenv('username'),'DangerZone')
        directory = 'E:\data\Recordings\';
    elseif strcmp(getenv('username'),'Radu')
        directory = 'E:\Spike_Sorting\';
    elseif strcmp(getenv('username'),'The Doctor')
        directory = 'C:\Users\The Doctor\Data\';
    elseif strcmp(getenv('username'),'JuanandKimi')
        directory = 'C:\Data\Recordings\';
    else
        directory = 'B:\data\Recordings\';
    end

cd([directory, 'spike2temp\']);

load('postss.mat'); % post simple spike data

% Variables from Spike2, uncomment for debugging
% ssclus = 1;
% timelength = 1377;
% tsamp = 5e-6;

tn1 = whos; % temporary name holder
tn2 = tn1.name;

eval(['datastr = ', tn2,';']); % get data as a struct
data = datastr.values;
data = data';

Fsamp = tsamp^(-1);
data_fft = fft(data);
[rws,cls] = size(data_fft);


mynewlabels = ones(1,cls).*double(ssclus);
        
whatttodo = 'fft_max_sd';
switch whatttodo
    case 'fft_max_1hz'
        
        data_fft_amp = abs(data_fft(1:(floor(rws/2)+1),:)); %get fft amplitudes
        
        freqs = linspace(0,Fsamp/2,(floor(rws/2)+1));
        llim = find(freqs > 0); llim = llim(1);
        rlim = find(freqs < 5000); rlim = rlim(end);
        
        data_fft_amp = data_fft_amp(llim:rlim,:);
        
        data_fft_maxes = max(data_fft_amp);
        [count_maxes,bin_centers] = hist(data_fft_maxes,1000);

        timelength = round(timelength);
        cutoff = sum(count_maxes)-timelength;

        cumul_hist = cumsum(count_maxes);

%       figure(1);
%       plot(bin_centers(count_maxes ~= 0),count_maxes(count_maxes ~= 0),'ko');
%       hold on;
%       plot(bin_centers(cumul_hist>cutoff),count_maxes(cumul_hist>cutoff),'r+');

        fft_cutoff = bin_centers(cumul_hist>cutoff);
        fft_cutoff = fft_cutoff(1);
        
        mynewlabels(data_fft_maxes >= fft_cutoff) = ssclus+30;
    
    case 'fft_sum_3sd'
        
        data_fft_amp = abs(data_fft(1:(floor(rws/2)+1),:)); %get fft amplitudes
        
        freqs = linspace(0,Fsamp/2,(floor(rws/2)+1));
        llim = find(freqs > 0); llim = llim(1);
        rlim = find(freqs < 4000); rlim = rlim(end);
        
        data_fft_amp = data_fft_amp(llim:rlim,:);
        
        data_fft_sum = sum(data_fft_amp);
        
        [muhat,sigmahat] = normfit(data_fft_sum');
        cutoff = muhat+3*sigmahat;
        
        mynewlabels(data_fft_sum >= cutoff) = ssclus+30;
        
    otherwise %fft_max_sd
        
        data_fft_amp = abs(data_fft(1:(floor(rws/2)+1),:)); %get fft amplitudes
        
        freqs = linspace(0,Fsamp/2,(floor(rws/2)+1));
        llim = find(freqs > 0); llim = llim(1);
        rlim = find(freqs < 3000); rlim = rlim(end);
        
        data_fft_amp = data_fft_amp(llim:rlim,:);
        
        data_fft_maxes = max(data_fft_amp);
        
        [muhat,sigmahat] = normfit(data_fft_maxes');
        cutoff = muhat+4*sigmahat;
        
        mynewlabels(data_fft_maxes >= cutoff) = ssclus+30;
        
end
