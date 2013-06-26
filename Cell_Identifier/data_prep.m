function out = data_prep(noise_est)

cd('E:\\Spike_Sorting\\spike2temp\\');

% load('holdisi.mat'); % post simple spike data
% tn1 = whos; % temporary name holder
% tn2 = tn1.name;
% eval(['isi = ', tn2,';']); % get data as a struct
% clearvars -except isi newname

load('holdwaves.mat');
tn1 = whos; % temporary name holder
tn2 = tn1.name;
eval(['waves = ', tn2,';']); % get data as a struct
[subj, coord, depth] = extract_info(tn2);
clearvars -except waves subj coord depth noise_est

isi = diff(waves.times);
isi_kurt = kurtosis(isi);
isi_skew = skewness(isi);
isi_std = std(isi);
isi_bar = mean(isi);
isi_med = median(isi);

mu = mean(waves.values);
[pks,pklocs] = findpeaks(mu);
[trs,trlocs] = findpeaks(-mu);
maxi = max(pks);
mini = -max(trs);
pk2pk = maxi-mini;

htlim = 0.1*pk2pk; %minimum height for a peak/trough

[pks,pklocs] = findpeaks(mu,'minpeakheight',htlim);
[trs,trlocs] = findpeaks(-mu,'minpeakheight',htlim);
% if maxiidx < miniidx
%     beginx = find(mu>noise_est); beginx = beginx(1);
%     endx = find(mu<-noise_est); endx = endx(end);
%     wid = (endx-beginx).*waves.interval;
% else
%     beginx = find(mu<-noise_est); beginx = beginx(1);
%     endx = find(mu>noise_est); endx = endx(end);
%     wid = (endx-beginx).*waves.interval;
% end

ptlocs = sort([pklocs,trlocs]);
if ismember(ptlocs(1),pklocs)
    beginx = find(mu>htlim); beginx = beginx(1);
else
    beginx = find(mu<-htlim); beginx = beginx(1);
end
if ismember(ptlocs(end),pklocs)
    endx = find(mu>htlim); endx = endx(end);
else
    endx = find(mu<-htlim); endx = endx(end);
end
wid = (endx-beginx).*waves.interval;
    
out = unit('unclassified',maxi,mini,pk2pk,wid,isi_kurt,isi_skew,isi_std,isi_bar,isi_med,depth,coord.lm,coord.ap);
end