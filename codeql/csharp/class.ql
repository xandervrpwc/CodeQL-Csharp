/**
 * @name class names
 */

 import csharp

 from File f, Class c
 where f.fromSource() and c.getFile() = f
 select f.getBaseName() as filename, c.getName() as code
