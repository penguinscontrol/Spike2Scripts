
%Plotaspike Summary of this function goes here
%   Detailed explanation goes here
figure();
plot(waves.values(plotspike,:));
hold all;
plot([0,waves.items],2.*[noise_est noise_est],'r-');
plot([0,waves.items],2.*[-noise_est -noise_est],'r-');
plot(find(waves.values(plotspike,:)==maxi(plotspike)),maxi(plotspike),'r*');
plot(find(waves.values(plotspike,:)==mini(plotspike)),mini(plotspike),'r*');

