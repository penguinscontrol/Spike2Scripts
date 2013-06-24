function out = getwavefeat(in)
[in.min minidx] = min(in.values,[],2);

[in.max maxidx] = max(in.values,[],2);

in.wid = (maxidx(:,1)-minidx(:,1)).*in.interval;

in.pk2pk = in.max-in.min;

out = in;
end

