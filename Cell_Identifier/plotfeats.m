function plotfeats( units, feat1, feat2, feat3 )
% plots the contents of cell array (items of the type unit)
if nargin == 2
if isprop(units(1,1),feat1)
    figure();
    [r, c] = size(units);
    hold all;
    
    unc = [];
    gol = [];
    den = [];
    ub = [];
    bas = [];
    ste = [];
    gra = [];
    bor = [];
    pur = [];
    fib = [];
    
    ha = zeros(1,10);
    for a = 1:r
        switch units(a).label
            case 'unclassified'
                unc = [unc units(a).(feat1)];
            case 'golgi'
                gol = [gol units(a).(feat1)];               
            case 'dentate'
                den = [den units(a).(feat1)];           
            case 'purkinje'
                pur = [pur units(a).(feat1)];              
            case 'fiber'
                fib = [fib units(a).(feat1)];              
            case 'ub'
                ub = [ub units(a).(feat1)];              
            case 'basket'
                bas = [bas units(a).(feat1)];              
            case 'stellate'
                ste = [ste units(a).(feat1)];              
            case 'granule'
                gra = [gra units(a).(feat1)];              
            case 'border'
                bor = [bor units(a).(feat1)];                
        end        
    end
    
    his = cell(1,10);
    hisbins = cell(1,10);
    
    if ~isempty(unc)
        [his{1},hisbins{1}] = hist(unc,1000);
        ha(1) = stem(hisbins{1}(his{1}~= 0),his{1}(his{1}~= 0),'ko','DisplayName','Unclassified');
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
    if ~isempty(ub)
        [his{6},hisbins{6}] = hist(ub,1000);
        ha(6) = stem(hisbins{6}(his{6}~= 0),his{6}(his{6}~= 0),'m+','DisplayName','Unipolar Brush');
    end
    if ~isempty(bas)
        [his{7},hisbins{7}] = hist(bas,1000);
        ha(7) = stem(hisbins{7}(his{7}~= 0),his{7}(his{7}~= 0),'m+','DisplayName','Basket');
    end
    if ~isempty(ste)
        [his{8},hisbins{8}] = hist(ste,1000);
        ha(8) = stem(hisbins{8}(his{8}~= 0),his{8}(his{8}~= 0),'m+','DisplayName','Stellate');
    end
    if ~isempty(gra)
        [his{9},hisbins{9}] = hist(gra,1000);
        ha(9) = stem(hisbins{9}(his{9}~= 0),his{9}(his{9}~= 0),'m+','DisplayName','Granule');
    end
    if ~isempty(bor)
        [his{10},hisbins{10}] = hist(bor,1000);
        ha(10) = stem(hisbins{10}(his{10}~= 0),his{10}(his{10}~= 0),'m+','DisplayName','Border');
    end
     
    
    xlabel(feat1);
    legend(ha(ha ~= 0),0);
    
    print('-djpeg',[feat1, '_hist']);
else
    error('Not a feature!');
end    
elseif nargin == 3

if isprop(units(1,1),feat1)&&isprop(units(1,1),feat2)
    figure();
    [r, c] = size(units);
    hold all;
    
    ha = zeros(1,10);
    for a = 1:r
        if ~isempty(units(a))
        switch units(a).label
            case 'unclassified'
                if ha(1) == 0
                    ha(1) = plot(units(a).(feat1),units(a).(feat2),'ko','DisplayName','Unclassified');
                else
                    plot(units(a).(feat1),units(a).(feat2),'ko');
                end
            case 'golgi'
                if ha(2) == 0
                    ha(2) = plot(units(a).(feat1),units(a).(feat2),'rs','DisplayName','Golgi');
                else
                    plot(units(a).(feat1),units(a).(feat2),'rs');
                end               
            case 'dentate'
                if ha(3) == 0
                    ha(3) = plot(units(a).(feat1),units(a).(feat2),'b*','DisplayName','Dentate');
                else
                    plot(units(a).(feat1),units(a).(feat2),'b*');
                end           
            case 'purkinje'
                if ha(4) == 0
                    ha(4) = plot(units(a).(feat1),units(a).(feat2),'gd','DisplayName','Purkinje');
                else
                    plot(units(a).(feat1),units(a).(feat2),'gd');
                end              
            case 'fiber'
                if ha(5) == 0
                    ha(5) =  plot(units(a).(feat1),units(a).(feat2),'m+','DisplayName','Fiber');
                else
                    plot(units(a).(feat1),units(a).(feat2),'m+');
                end              
            case 'ub'
                if ha(6) == 0
                    ha(6) =  plot(units(a).(feat1),units(a).(feat2),'m+','DisplayName','Unipolar Brush');
                else
                    plot(units(a).(feat1),units(a).(feat2),'m+');
                end              
            case 'basket'
                if ha(7) == 0
                    ha(7) =  plot(units(a).(feat1),units(a).(feat2),'m+','DisplayName','Basket');
                else
                    plot(units(a).(feat1),units(a).(feat2),'m+');
                end              
            case 'stellate'
                if ha(8) == 0
                    ha(8) =  plot(units(a).(feat1),units(a).(feat2),'m+','DisplayName','Stellate');
                else
                    plot(units(a).(feat1),units(a).(feat2),'m+');
                end              
            case 'granule'
                if ha(9) == 0
                    ha(9) =  plot(units(a).(feat1),units(a).(feat2),'m+','DisplayName','Granule');
                else
                    plot(units(a).(feat1),units(a).(feat2),'m+');
                end              
            case 'border'
                if ha(10) == 0
                    ha(10) =  plot(units(a).(feat1),units(a).(feat2),'m+','DisplayName','Border');
                else
                    plot(units(a).(feat1),units(a).(feat2),'m+');
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
if isprop(units(1,1),feat1)&&isprop(units(1,1),feat2)&&isprop(units(1,1),feat3)
    figure();
    [r, c] = size(units);
    hold all;
    
    ha = zeros(1,10);
    for a = 1:r
        switch units(a).label
            case 'unclassified'
                if ha(1) == 0
                    ha(1) = plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'ko','DisplayName','Unclassified');
                else
                    plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'ko');
                end
            case 'golgi'
                if ha(2) == 0
                    ha(2) = plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'rs','DisplayName','Golgi');
                else
                    plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'rs');
                end               
            case 'dentate'
                if ha(3) == 0
                    ha(3) = plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'b*','DisplayName','Dentate');
                else
                    plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'b*');
                end           
            case 'purkinje'
                if ha(4) == 0
                    ha(4) = plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'gd','DisplayName','Purkinje');
                else
                    plot(units(a).(feat1),units(a).(feat2),'gd');
                end              
            case 'fiber'
                if ha(5) == 0
                    ha(5) =  plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+','DisplayName','Fiber');
                else
                    plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+');
                end              
            case 'ub'
                if ha(6) == 0
                    ha(6) =  plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+','DisplayName','Unipolar Brush');
                else
                    plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+');
                end               
            case 'basket'
                if ha(7) == 0
                    ha(7) =  plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+','DisplayName','Basket');
                else
                    plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+');
                end               
            case 'stellate'
                if ha(8) == 0
                    ha(8) =  plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+','DisplayName','Stellate');
                else
                    plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+');
                end               
            case 'granule'
                if ha(9) == 0
                    ha(9) =  plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+','DisplayName','Granule');
                else
                    plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+');
                end               
            case 'border'
                if ha(10) == 0
                    ha(10) =  plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+','DisplayName','Border');
                else
                    plot3(units(a).(feat1),units(a).(feat2),units(a).(feat3),'m+');
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

