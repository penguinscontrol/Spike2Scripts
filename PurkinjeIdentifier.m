cd('E:\\Spike_Sorting\\spike2temp\\');
load('postss.mat'); % post simple spike data

tn1 = whos; % temporary name holder
tn2 = tn1.name;

eval(['datastr = ', tn2,';']); % get data as a struct
data = datastr.values;
plot(data');