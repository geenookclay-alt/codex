import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}
  canActivate(ctx: ExecutionContext): boolean {
    const required = this.reflector.getAllAndOverride<string[]>('roles', [ctx.getHandler(), ctx.getClass()]) || [];
    if (!required.length) return true;
    const req = ctx.switchToHttp().getRequest();
    return required.includes(req.user?.role);
  }
}
