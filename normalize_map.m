function out = normalize_map( in )
%% Called by spike shape heat map to normalize crossings on a scale from 0 to 1
in_max = max(max(in));
in = in./in_max;
out = ones(size(in))-exp(-5.*in);
end

