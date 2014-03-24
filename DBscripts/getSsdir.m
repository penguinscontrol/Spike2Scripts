function ssdir = getSsdir( conn )
%getSsdir queries database for this machine's spike sorting root directory
ssdirq = ['SELECT path FROM machines WHERE m_name = ''' getenv('username') ''''];
ssdir = fetch(conn,ssdirq); ssdir = ssdir{1};

end

