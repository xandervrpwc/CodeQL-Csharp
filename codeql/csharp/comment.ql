/**
 * @name commentlines
 */

 import csharp

 from File f, CommentLine cl
 select f.getBaseName() as filename, cl.getText() as code
