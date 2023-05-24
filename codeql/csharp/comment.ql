/**
 * @name commentlines
 */

 import csharp

 from File f, CommentLine cl
 where f.fromSource()
 select f.getBaseName() as filename, cl.getText() as code
