function chamber = getChamber(fname, conn)
%getChamber retrieves chamber location base on file name and session table
global subject;

part=regexpi(fname,'^*\d+', 'match'); part = part{1};
%q = ['SELECT s.location FROM sessions s INNER JOIN users u ON m.user_id_fk = u.user_id WHERE m_name = ''' getenv('username') ''''];
query = ['SELECT s.Location FROM sessions s WHERE Subject = ''' subject ''' and Part = ''' part ''''];
chamber = fetch(conn,query);

if isempty(chamber)
    chamber='UNKNOWN';
end

if size(chamber,1)>1 %annoying cases with two different recordings in same session
    %check if same chamber
    if strcmp(chamber{1},chamber{2})
        chamber=chamber(1);
    end
end
end

