function plotfeats2d( units, feat1, feat2, feat3 )
% plots the contents of cell array (items of the type unit)
if nargin == 2
if isprop(units{1,1},feat1)
    figure();
    [r, c] = size(units);
    hold all;
    
    unc = [];
    gol = [];
    den = [];
    pur = [];
    fib = [];
    
    ha = zeros(1,5);
    for a = 1:r
        switch units{a}.label
            case 'unclassified'
                unc = [unc units{a}.(feat1)];
            case 'Golgi'
                gol = [den units{a}.(feat1)];               
            case 'Dentate'
                den = [den units{a}.(feat1)];           
            case 'Purkinje'
                pur = [pur units{a}.(feat1)];              
            case 'Fiber'
                fib = [fib units{a}.(feat1)];           
        end        
    end
    
    his = cell(1,5);
    hisbins = cell(1,5);
    
    if ~isempty(unc)
        [his{1},hisbins{1}] = hist(unc,1000);
        ha(1) = stem(hisbins{1}(his{1}~= 0),his{1}(his{1}~= 0),'ko','DisplayName','unclassified');
    end
    if ~isempty(gol)
        [his{2},hisbins{2}] = hist(gol,1000);
        ha(2) = stem(hisbins{2}(his{2}~= 0),his{2}(his{2}~= 0),'rs','DisplayName','Golgi');
    end
    if ~isempty(den)
        [his{3},hisbins{3}] = hist(den,1000);
        ha(3) = stem(hisbins{3}(his{3}~= 0),his{3}(his{3}~= 0),'b*','DisplayName','Dentate');
    end
    if ~isempty(pur)
        [his{4},hisbins{4}] = hist(pur,1000);
        ha(4) = stem(hisbins{4}(his{4}~= 0),his{4}(his{4}~= 0),'gd','DisplayName','Purkinje');
    end
    if ~isempty(fib)
        [his{5},hisbins{5}] = hist(fib,1000);
        ha(5) = stem(hisbins{5}(his{5}~= 0),his{5}(his{5}~= 0),'m+','DisplayName','Fiber');
    end
     
    
    xlabel(feat1);
    legend(ha(ha ~= 0),0);
    
    print('-djpeg',[feat1, '_hist']);
else
    error('Not a feature!');
end    
elseif nargin == 3

if isprop(units{1,1},feat1)&&isprop(units{1,1},feat2)
    figure();
    [r, c] = size(units);
    hold all;
    
    ha = zeros(1,5);
    for a = 1:r
        if ~isempty(units{a})
        switch units{a}.label
            case 'unclassified'
                if ha(1) == 0
                    ha(1) = plot(units{a}.(feat1),units{a}.(feat2),'ko','DisplayName','unclassified');
                else
                    plot(units{a}.(feat1),units{a}.(feat2),'ko');
                end
            case 'Golgi'
                if ha(2) == 0
                    ha(2) = plot(units{a}.(feat1),units{a}.(feat2),'rs','DisplayName','Golgi');
                else
                    plot(units{a}.(feat1),units{a}.(feat2),'rs');
                end               
            case 'Dentate'
                if ha(3) == 0
                    ha(3) = plot(units{a}.(feat1),units{a}.(feat2),'b*','DisplayName','Dentate');
                else
                    plot(units{a}.(feat1),units{a}.(feat2),'b*');
                end           
            case 'Purkinje'
                if ha(4) == 0
                    ha(4) = plot(units{a}.(feat1),units{a}.(feat2),'gd','DisplayName','Purkinje');
                else
                    plot(units{a}.(feat1),units{a}.(feat2),'gd');
                end              
            case 'Fiber'
                if ha(5) == 0
                    ha(5) =  plot(units{a}.(feat1),units{a}.(feat2),'m+','DisplayName','Fiber');
                else
                    plot(units{a}.(feat1),units{a}.(feat2),'m+');
                end           
        end
        end
    end
    xlabel(feat1);
    ylabel(feat2);
    legend(ha(ha ~= 0),0);
    print('-djpeg',[feat1, '_vs_', feat2]);
else
    error('Not a feature!');
end

elseif nargin == 4
if isprop(units{1,1},feat1)&&isprop(units{1,1},feat2)&&isprop(units{1,1},feat3)
    figure();
    [r, c] = size(units);
    hold all;
    
    ha = zeros(1,5);
    for a = 1:r
        switch units{a}.label
            case 'unclassified'
                if ha(1) == 0
                    ha(1) = plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'ko','DisplayName','unclassified');
                else
                    plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'ko');
                end
            case 'Golgi'
                if ha(2) == 0
                    ha(2) = plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'rs','DisplayName','Golgi');
                else
                    plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'rs');
                end               
            case 'Dentate'
                if ha(3) == 0
                    ha(3) = plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'b*','DisplayName','Dentate');
                else
                    plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'b*');
                end           
            case 'Purkinje'
                if ha(4) == 0
                    ha(4) = plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'gd','DisplayName','Purkinje');
                else
                    plot(units{a}.(feat1),units{a}.(feat2),'gd');
                end              
            case 'Fiber'
                if ha(5) == 0
                    ha(5) =  plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'m+','DisplayName','Fiber');
                else
                    plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'m+');
                end           
        end        
    end
    xlabel(feat1);
    ylabel(feat2);
    zlabel(feat3);
    legend(ha(ha ~= 0),0);
    set(gca,'XGrid','on','YGrid','on');
    print('-djpeg',[feat1, '_vs_', feat2, '_vs_', feat3]);
else
    error('Not a feature!');
end    
end

end

