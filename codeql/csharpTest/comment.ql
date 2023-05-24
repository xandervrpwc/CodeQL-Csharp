/**
 * @name commentlines
 */

 import csharp

 from File f, CommentLine cl
 where f.fromSource() and f.getBaseName() in ["SecurityHeaderSettings.cs", "security.json", "UpdateRolePermissionsRequest.cs","TokenService.cs"]
 select f.getBaseName() as filename, cl.getText() as code
