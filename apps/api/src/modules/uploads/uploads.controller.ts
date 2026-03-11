import { Body, Controller, Get, Post, UseGuards } from '@nestjs/common';
import { UploadsService } from './uploads.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('uploads')
@UseGuards(JwtAuthGuard)
export class UploadsController {
  constructor(private readonly service: UploadsService) {}
  @Get()
  list() { return this.service.list(); }
  @Post()
  upsert(@Body() body: any) { return this.service.upsert(body); }
}
