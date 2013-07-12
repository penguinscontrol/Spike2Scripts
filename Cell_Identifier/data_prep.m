function out = data_prep(noise_est, plotting)

global act_name;

if strcmp(getenv('username'),'DangerZone')
        directory = 'E:\data\Recordings\';
    elseif strcmp(getenv('username'),'Radu')
        directory = 'E:\Spike_Sorting\';
    elseif strcmp(getenv('username'),'The Doctor')
        directory = 'C:\Users\The Doctor\Data\';
    else
        directory = 'B:\data\Recordings\';
    end

cd([directory, 'spike2temp\']);

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
if ~isempty(act_name)
    subj = act_name;
end
clearvars -except waves subj coord depth noise_est tn2 plotting

isi = diff(waves.times);
isi_kurt = kurtosis(isi);
isi_skew = skewness(isi);
isi_std = std(isi);
isi_bar = mean(isi);
isi_med = median(isi);
isi_cv = isi_std/isi_bar;

adjdiff = abs(diff(isi));
isi_1 = isi(2:end);
isi_0 = isi; isi_0(end) = [];
adjsum = isi_1+isi_0;
cv2 = 2.*adjdiff./adjsum;
med_cv2 = median(cv2);

mu = mean(waves.values);
[pks,pklocs] = findpeaks(mu);
[trs,trlocs] = findpeaks(-mu);
maxi = max(pks);
mini = -max(trs);
pk2pk = maxi-mini;

htlim = 0.15*pk2pk; %minimum height for a peak/trough

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

if plotting
    figure();
    x = [0:(waves.items-1)].*waves.interval;
    plot(x,mu,'ko');
    hold on;
    plot([0, (waves.items-1).*waves.interval],[htlim htlim],'r-');
    plot([0, (waves.items-1).*waves.interval],[-htlim -htlim],'r-');
    
    plot((beginx-1).*waves.interval,mu(beginx),'g*');
    plot((endx-1).*waves.interval,mu(endx),'g*');
    
    plot((pklocs-1).*waves.interval,pks,'r*');
    plot((trlocs-1).*waves.interval,-trs,'r*');
end

out = unit('unclassified',maxi,mini,pk2pk,wid,isi_kurt,isi_skew,isi_std,isi_bar,isi_med,isi_cv,med_cv2,depth,coord.lm,coord.ap);
end