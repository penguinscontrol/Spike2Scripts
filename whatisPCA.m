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


code = datastr.codes(:,1);
ucode = unique(code);

data = data(1:100,:);
code = code(1:100,:)
Fsamp = tsamp^(-1);

[COEFF, SCORE] = pca(data);
mean_wave = mean(data);
figure(1);

for a = 1:length(ucode)
    comp1 = SCORE(:,1);
    comp2 = SCORE(:,2);
    comp3 = SCORE(:,3);
    scatter3(comp1(code == ucode(a)),comp2(code == ucode(a)),comp2(code == ucode(a)),'.',...
        'MarkerEdgeColor',[a/length(ucode),(length(ucode)-a)/length(ucode),a/length(ucode)]); 
    hold on;   
end

whatqs = [10 30 50 70 90].*1e-2;
for a = 1:3
    [muhat,sigmahat] = normfit(SCORE(:,a));
	q{a} = ones(1,5).*muhat+[-3 -1.5 0 1.5 3].*sigmahat;
end

[x, y, z] = meshgrid(q{1},q{2},q{3});
 xl = reshape(x,1,size(x,1)*size(x,2)*size(x,3));
 yl = reshape(y,1,size(y,1)*size(y,2)*size(y,3));
 zl = reshape(z,1,size(z,1)*size(z,2)*size(z,3));
 
 
 scatter3(xl,yl,zl,'o');
 hands = cell(size(x,1),size(x,2),size(x,3));
 count = 1;
 for a = 1:size(x,1)
     figure(a+1);
     for b = 1:size(x,2)*size(x,3)
        thisscore = [xl(a) yl(a) zl(a) zeros(1,size(COEFF,2)-3)];
        thiswave = mean_wave+thisscore*COEFF';
        subplot(size(x,2),size(x,3),b);
        hands{count} = plot(thiswave);
        count = count+1;
     end        
 end
 
 figure(1)
 xlabel('Comp1');
 ylabel('Comp2');
 zlabel('Comp3');
 for a = 1:length(xl)
     text(xl(a),yl(a),zl(a),['  f',num2str(mod(a,size(x,1)))])%,'r',num2str(mod(a,size(x,2))),'c',num2str(mod(a,size(x,3)))]);
 end