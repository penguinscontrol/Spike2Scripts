function fcomments = getComments( fname, conn )
%getComments retrieves comments for a particular file from a txt file in
%the file's directory
fcomments = '';
subj = whichSubj(fname(1));
ssdir = getSsdir( conn );

fhandle = fopen([ssdir subj '\comments.txt']);
    if fhandle ~= -1
        thisline = fgetl(fhandle);
        foundit = false;
        done = false;
        while ischar(thisline) && (~foundit || ~done)
            if ~isempty(regexp(thisline, fname)) && ~foundit
                foundit = true;
            end
            
            thisline = fgetl(fhandle);
            if ~ischar(thisline)
                continue;
            end
            
            if ~isempty(regexp(thisline, '.smr'))
                done = true;
            end
            
            if foundit && ~done
                fcomments = [fcomments sprintf('\n') thisline];
            end
        end
        fclose(fhandle);
    end
    if isempty(fcomments)
        fcomments = ' ';
    end
end

