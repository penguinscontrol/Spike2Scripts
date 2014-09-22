function user = getUser( conn )
%getUser retrieves current user name based on environmental variable user
%from the database
q = ['SELECT u.name FROM machines m INNER JOIN users u ON m.user_id_fk = u.user_id WHERE m_name = ''' getenv('username') ''''];
user = fetch(conn,q); user = user{1};

end

