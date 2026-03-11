import { Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
@Injectable()
export class AuthService {
  constructor(private jwt: JwtService) {}
  login(userId: string, role: string) { return { access_token: this.jwt.sign({ sub: userId, role }) }; }
}
