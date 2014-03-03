% if strcmp(getenv('username'),'DangerZone')
%         directory = 'E:\data\Recordings\';
%     elseif strcmp(getenv('username'),'Radu')
%         directory = 'E:\Spike_Sorting\';
%     elseif strcmp(getenv('username'),'The Doctor')
%         directory = 'C:\Users\The Doctor\Data\';
%     elseif strcmp(getenv('username'),'JuanandKimi')||...
%             strcmp(getenv('username'),'Purkinje');
%         directory = 'C:\Data\Recordings\';
%     else
%         directory = 'B:\data\Recordings\';
%     end

cd([directory, 'spike2temp\']);
load('for3Ddraw.mat');

testing = 0;

% incoming variables from Spike2. Uncomment for debugging.
% tsamp = 2.5e-5;

tn1 = whos; % temporary name holder
tn2 = tn1.name;

eval(['data = ', tn2,';']); % get data as a struct

cfig = 1;
xsize = 512;
ysize = 512;
if testing
data.values = data.values(1:500,:);
end
trange = [1:data.items].*tsamp.*1e3;
vrange = 1.01.*[min(min(data.values)) max(max(data.values))];
vrange = linspace(vrange(1),vrange(2),xsize);
ext_trange = linspace(trange(1),trange(end),ysize);

splined_data = spline(trange,data.values,ext_trange);

[T,V] = meshgrid(ext_trange, vrange);
M = zeros(length(vrange),length(ext_trange));
[rows, cols] = size(splined_data);
for b = 1:rows
        curspike = splined_data(b,:);
    for c = 1:length(ext_trange)
        for d = 1:(length(vrange)-1)
            if (curspike(c)>vrange(d) && curspike(c)<vrange(d+1))
                M(d,c) = M(d,c)+1;
            end
        end
    end
end
figure(cfig); cfig = cfig+1;

M = normalize_map(M);

colormap('bone')
surf(T,V,M);
shading interp;
view(2);
axis off;
axis([0,trange(end),vrange(1),vrange(end)]);
set(gcf,'Color','Black');
set(gca,'Color','Black');
grid off;