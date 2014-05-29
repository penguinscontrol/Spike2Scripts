function sp2list = existingSortSp2Dlg( who_by, fname )
%existingSortSp2Dlg Creates the prompt for a sp2 dialog box using existing
%sorts

sp2list = '';
for a = 1:size(who_by,1)
    sp2list = [sp2list fname{a} ' by ' who_by{a} '|'];
end
sp2list(end) = [];

end

