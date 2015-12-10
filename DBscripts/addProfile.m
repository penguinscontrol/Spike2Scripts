function success = addProfile(profiles, profiletypes, clusids, conn )
%addProfile adds or modify profiles in the cluster table
     
try
col_names = {'profile','profile_type'};
% update(conn,'clusters',col_names,{profiles,profiletypes},['WHERE cluster_id IN ' clusids]);

for dataitem=1:size(profiles,1)
ci=clusids(dataitem);
prof=profiles{dataitem}; %varchar 
proft=profiletypes(dataitem); %smallint

update(conn,'clusters',col_names,{prof,proft},['WHERE cluster_id = ' num2str(ci) ';']);
commit(conn)

end
    success = true;
catch
    success = false;
end

end

