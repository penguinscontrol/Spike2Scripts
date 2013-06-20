function out = normalize_map( in )
in_max = max(max(in));
in = in./in_max;
out = ones(size(in))-exp(-5.*in);
end

