
cd('E:\\Spike_Sorting\\spike2temp\\');

load('postss.mat'); % post simple spike data

%ssclus = 1;
%timelength = 1377;

tn1 = whos; % temporary name holder
tn2 = tn1.name;

eval(['datastr = ', tn2,';']); % get data as a struct
data = datastr.values;
data = data';

data_fft = fft(data);
[rws,cls] = size(data_fft);
data_fft_amp = abs(data_fft(2:(floor(rws/2)+1),:)); %get fft amplitudes, minus DC offset

data_fft_maxes = max(data_fft_amp);
[count_maxes,bin_centers] = hist(data_fft_maxes,1000);

timelength = round(timelength);
cutoff = sum(count_maxes)-timelength;

cumul_hist = cumsum(count_maxes);

figure(1);
plot(bin_centers(count_maxes ~= 0),count_maxes(count_maxes ~= 0),'ko');
hold on;
plot(bin_centers(cumul_hist>cutoff),count_maxes(cumul_hist>cutoff),'r+');

fft_cutoff = bin_centers(cumul_hist>cutoff);
fft_cutoff = fft_cutoff(1);

mynewlabels = ones(1,cls).*double(ssclus);

mynewlabels(data_fft_maxes >= fft_cutoff) = ssclus+30;

text(bin_centers(count_maxes == max(count_maxes)),count_maxes(count_maxes == max(count_maxes)),sprintf('This is working!'));