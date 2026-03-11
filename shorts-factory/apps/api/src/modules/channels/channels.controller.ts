import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { ChannelsService } from './channels.service';
import { CreateChannelsDto } from './dto/create-channels.dto';
import { ChannelsEntity } from './entity/channels.entity';
import { JwtGuard } from '../../common/jwt.guard';

@UseGuards(JwtGuard)
@Controller('channels')
export class ChannelsController {
  constructor(private readonly service: ChannelsService) {}

  @Get()
  findAll(): Promise<ChannelsEntity[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<ChannelsEntity | null> {
    return this.service.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateChannelsDto): Promise<ChannelsEntity> {
    return this.service.create(dto);
  }
}
