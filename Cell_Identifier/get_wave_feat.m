function [mini, maxi, pk2pk, wid] = getwavefeat(in)
[mini minidx] = min(in.values,[],2);

[maxi maxidx] = max(in.values,[],2);

wid = (maxidx(:,1)-minidx(:,1)).*in.interval;

pk2pk = maxi-mini;
end

