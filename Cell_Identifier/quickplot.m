clear; clc; cfig = 1;
figure(cfig); cfig = cfig+1;
x = load_folder('C:\Users\The Doctor\Data\Rigel\Features');
y = load_folder('C:\Users\The Doctor\Data\Sixx\Features');
z = load_folder('C:\Users\The Doctor\Data\Hilda\Features');
t = load_training_set;
alu = [x;y;z];

faking = 1;
if faking
    for a = 1:length(x)
        x{a}.label = 'Golgi';
    end
    for a = 1:length(y)
        y{a}.label = 'Purkinje';
    end
    for a = 1:length(z)
        z{a}.label = 'Dentate';
    end
end

for a = 1:length(t)
    if strcmp(t{a}.label,'Purkinje')
        p{a} = t{a};
    end
end

for a = 1:length(p)
    if ~isempty(p{a})
        p_isi(a) = p{a}.isi_med.^(-1);
        p_cv2(a) = p{a}.med_cv2;
    end
end

p_isi = p_isi(p_isi~=0);
p_cv2 = p_cv2(p_cv2~=0);

for a = 1:length(alu)
    if ~isempty(alu{a})
    alu_isi(a) = alu{a}.isi_med.^(-1);
    alu_cv2(a) = alu{a}.med_cv2;
    end
end

alu_isi = alu_isi(alu_isi~=0);
alu_cv2 = alu_cv2(alu_cv2~=0);

hold on;
plot(alu_isi,alu_cv2,'ko');
plot(p_isi,p_cv2,'k*');
ylabel('Median CV2');
xlabel('Median firing rate (spk/s)');
legend('Unclassified','Purkinje');
axis([0 180 0 0.7])

for a = 1:length(alu)
    allunits(a) = alu{a}
end

