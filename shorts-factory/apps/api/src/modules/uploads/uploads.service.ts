import { Injectable } from '@nestjs/common';
import { CreateUploadsDto } from './dto/create-uploads.dto';
import { UploadsEntity } from './entity/uploads.entity';

@Injectable()
export class UploadsService {
  async findAll(): Promise<UploadsEntity[]> { return []; }
  async findOne(id: string): Promise<UploadsEntity | null> { return { id, name: 'uploads' } as UploadsEntity; }
  async create(dto: CreateUploadsDto): Promise<UploadsEntity> {
    return { id: crypto.randomUUID(), name: dto.name ?? 'uploads' } as UploadsEntity;
  }
}
