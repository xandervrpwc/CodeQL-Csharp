/**
 * @name class names
 */

 import csharp

 from File f, Class c
 where f.fromSource() and c.getFile() = f and f.getBaseName() in ["SecuritySettings.cs", "security.json", "UpdateRolePermissions.cs","TokenService.cs"]
 select f.getBaseName() as filename, c.getName() as code
