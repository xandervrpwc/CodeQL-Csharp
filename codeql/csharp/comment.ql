/**
 * @name comments
 */

 import csharp

 from File f, CommentBlock cb
 where f.fromSource()
 select f.getBaseName() as filename, cb as code
