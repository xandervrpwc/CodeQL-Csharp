/**
 * @name commentlines
 */

 import csharp

 from File f, CommentLine cl
 where f.fromSource() and f.getBaseName() in ["SecuritySettings.cs", "security.json", "UpdateRolePermissions.cs","TokenService.cs"]
 select f.getBaseName() as filename, cl.getText() as code
