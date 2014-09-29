function session = whichSession( init, part , conn )
% whichSession
% what is the session index for a given subject and session (part) number

subj = whichSubj(init);
query = ['SELECT s.sessions_id FROM sessions s WHERE Subject = ''' subj ''' and Part = ''' part ''''];           
session = fetch(conn,query);

end

