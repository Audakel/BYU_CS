/**
* Non-drive entity must be contained in another entity.
* These entities, very much like their “real” file-system counterparts, obey the following relations.
* Every entity has the following properties
* 
*/
public abstract class Entry {
	/** entity A contains entity B then we say that A is the parent of B. */
	protected Drive parent;
	/** The type of the entity */
	protected EntryType type;	
	/** The type of the entity (one of the 4 @EntryType below). */
	protected String name;
	/** An alphanumeric string. Two entities with the same parent cannot have the same name.  */
	protected double size;
	/** size of item, depends on what entry type it is */
	protected long created;
	/** time stamp of last update */
	protected long lastUpdated;
	/** time stamp of last access */
	protected long lastAccessed;

	/**
	* The type of the entity
	*/
	protected enum EntryType {
	    DRIVE,
	    FOLDER,
	    FILE,
	    ZIP;
	}

	/**
	* Creates a new entity.
	* Non-drive entity must be contained in another entity.
	* Every entity has the properties
	* 
	* @param	path: The concatenation of the names of the containing entities, from the drive down to file
	* @param	type: The type of the entity (one of the 4 type above).
	* @param 	name: An alphanumeric string. Two entities with the same parent cannot have the same name. 
	*					Similarly, two drives cannot have the same name.
	* @return   An entry
	*/
	public Entry(String n, Directory p, EntryType t) {
		if (parent == null) {
			throw new PathNotFoundException();
		}
		if (pathExists(p + "/" + n)) {
			throw new PathAlreadyExistsException();
		}

		name = n;
		parent = p;
		type = t;
		created = System.currentTimeMillis();
		lastUpdated = System.currentTimeMillis();
		lastAccessed = System.currentTimeMillis();
	}

	/**
	* Deletes an existing entity (and all the entities it contains).
	*
	* @param		path: The concatenation of the names of the containing entities, from the drive down to file
	* @exception 	PathNotFoundException 
	*/
	public boolean delete(String path) {
		if (parent == null) {
			throw new PathNotFoundException();
		}
		return parent.deleteEntry(this);
	}

	public abstract int size();

	/** 
	* Changing the parent of an entity.
	*
	* @param		sp: Source Path
	* @param 		dp: Destination Path.
	* @exception 	PathAlreadyExistsException
	*/
	public void move(String sp, String dp){
		if (pathExists(dp)) throw new PathAlreadyExistsException();

		if (getParent(sp) == FILE) throw new IllegalFileSystemOperationException();

		switch (type) {
            case DRIVE:  
            	if (isRootDir(p)) this.setPath(p)
            	break;
    	    case FOLDER:  
            	this.setPath(p)
            	break;	
    	    case FILE:  
            	this.setPath(p)
            	break;            		
    	    case ZIP:  
            	this.setPath(p)
            	break;
        	default:
        		throw new IllegalFileSystemOperationException();
                break;
        }
		
	}

	public String getFullPath() {
		if (parent == null) return name;
		else return parent.getFullPath() + "/" + name;
	}

	public String setFullPath() {
		if (parent == null) return name;
		else return parent.getFullPath() + "/" + name;
	}

	public long getCreationTime() {
		return created;
	}

	public long getLastUpdatedTime() {
		return lastUpdated;
	}

	public long getLastAccessedTime() {
		return lastAccessed;
		public void changeName(String n) {
			name = n;
		}
		public String getName() {
			return name;
		}
	}

	/**
	* A file does not contain any other entity, just text
	* 
	* @param	directory: The concatenation of the names of the containing entities, from the drive down to file
	* @param	size: The size of the containing entities
	* @param 	name: An alphanumeric string. Two entities with the same parent cannot have the same name. 
	*					Similarly, two drives cannot have the same name.
	* @return   A File
	*/
	public class File extends Entry {
		/**
		* A text file has a property called Content which is a string.
		*/
		private String content;

		public File(String n, Directory p, int sz) {
			super(n, p);
			size = sz;
		}

		/**
		* Length of its content.
		*/
		public int size() {
			return getContents().length();
		}

		/** 
		*  Changes the content of a text file.
		*/
		public void writeToFile(String c) {
			content = c;
		}
		public String getContents() {
			return content;
		}

	}

	/**
	* A drive is not contained in any entity.
	* 
	* @param	type: The type of the entity (one of the 4 type above).
	* @param 	name: An alphanumeric string. Two entities with the same parent cannot have the same name. 
	*					Similarly, two drives cannot have the same name.
	* @return   A Drive
	*/
	public class Drive extends Entry {
		private String content;

		public Drive(String n) {
			super(n, null);
			size = sz;
		}
		/**
		* count of its content.
		*/
		public int size() {
			return size;
		}
		public String getContents() {
			return content;
		}
		public void setContents(String c) {
			content = c;
		}
	}

	/**
	* A folder,
	* May contain zero to many other folders, or files (text or zip)
	*
	* @param	path: The concatenation of the names of the containing entities, from the drive down to file
	* @param	type: The type of the entity (one of the 4 type above).
	* @param 	name: An alphanumeric string. Two entities with the same parent cannot have the same name. 
	*					Similarly, two drives cannot have the same name.
	* @return   A Folder
	*/
	public class Folder extends Entry {
		protected ArrayList < Entry > contents;

		public Folder(String n, Directory p) {
			super(n, p);
			contents = new ArrayList < Entry > ();
		}
		/**
		* Count of its content.
		*/
		public int size() {
			int size = 0;
			for (Entry e: contents) {
			 size += e.size();
			}
			return size;
		}

		public int numberOfFiles() {
			int count = 0;
			for (Entry e: contents) {
			 if (e instanceof Directory) {
			  count++; 
			  Directory d = (Directory) e;
			  count += d.numberOfFiles();
			 } else if (e instanceof File) {
			  count++;
			 }
			}
			return count;
		}

		public boolean deleteEntry(Entry entry) {
			return contents.remove(entry);
		}

		public void addEntry(Entry entry) {
			contents.add(entry);
		}

		protected ArrayList < Entry > getContents() {
			return content;
		}
	}

	/**
	* zip must be contained in another entity.
	* Every zip has the following properties:
	* 
	* @param	path: The concatenation of the names of the containing entities, from the drive down to file
	* @param	type: The type of the entity (one of the 4 type above).
	* @param 	name: An alphanumeric string. Two entities with the same parent cannot have the same name. 
	*					Similarly, two drives cannot have the same name.
	* @return   A zip
	*/
	public class Zip extends Directory {

		public Zip(String n, Directory p) {
			super(n, p);
			contents = new ArrayList < Entry > ();
		}

		/**
		*  One half of the sum of all sizes of the entities it contains.
		*/ 
		@Override
		public int size() {
			int size = 0;
			for (Entry e: contents) {
			 size += e.size();
			}
			return size / 2;
		}
	}
}



