clear;clc;

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

load('fortesting.mat'); % post simple spike data

% Variables from Spike2, uncomment for debugging
timelength = 518.160;
tsamp = 2e-5;

tn1 = whos; % temporary name holder
tn2 = tn1.name;

eval(['datastr = ', tn2,';']); % get data as a struct
data = datastr.values;
data = data;

Fsamp = tsamp^(-1);

[COEFF, SCORE] = pca(data);
mean_wave = mean(data);


whatqs = [10 30 50 70 90].*1e-2;
for a = 1:3
	q{a} = quantile(SCORE(:,a),whatqs);
end

[x, y, z] = meshgrid(q{1},q{2},q{3});
 x = reshape(x,1,size(x,1)*size(x,2)*size(x,3));
 y = reshape(y,1,size(y,1)*size(y,2)*size(y,3));
 z = reshape(z,1,size(z,1)*size(z,2)*size(z,3));
 
 for a = 1:length(x)
     figure();
     thiswave = mean_wave+x(a).*COEFF(1,:)+y(a).*COEFF(2,:)+z(a).*COEFF(3,:);
     plot(thiswave);
 end