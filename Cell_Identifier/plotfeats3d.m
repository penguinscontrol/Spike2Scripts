function plotfeats2d( units, feat1, feat2, feat3 )
% plots the contents of cell array (items of the type unit)
if isprop(units{1,1},feat1)&&isprop(units{1,1},feat2)
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
                    ha(2) = plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'ks','DisplayName','Golgi');
                else
                    plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'ks');
                end               
            case 'Dentate'
                if ha(3) == 0
                    ha(3) = plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'k*','DisplayName','Dentate');
                else
                    plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'k*');
                end           
            case 'Purkinje'
                if ha(4) == 0
                    ha(4) = plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'kd','DisplayName','Purkinje');
                else
                    plot(units{a}.(feat1),units{a}.(feat2),'kd');
                end              
            case 'Fiber'
                if ha(5) == 0
                    ha(5) =  plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'k+','DisplayName','Fiber');
                else
                    plot3(units{a}.(feat1),units{a}.(feat2),units{a}.(feat3),'k+');
                end           
        end        
    end
    xlabel(feat1);
    ylabel(feat2);
    zlabel(feat3);
    legend(ha(ha ~= 0),0);
    set(gca,'XGrid','on','YGrid','on');
else
    error('Not a feature!');
end

end

